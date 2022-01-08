from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import render, get_object_or_404

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_403_FORBIDDEN
from rest_framework import parsers, renderers, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from base.perms import IsAdminAPI

from base.serializers import KeySerializer, AuthSerializer
from voting.serializers import VotingSerializer
from .serializers import AdminQuestionSerializer, AdminVotingGetSerializer, AdminVotingSerializer, CensusSerializer, UserAdminSerializer, UserSerializer, UserUpdateSerializer

from base.models import Auth, Key
from voting.models import Question, Voting, QuestionOption
from census.models import Census

from utils.utils import is_valid


def index(request):
    return render(request, "build/index.html")


class DashboardAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request):
        n_of_users = User.objects.count()
        n_of_active_users = User.objects.filter(is_active=True).count()
        n_of_admins = User.objects.filter(is_superuser=True).count()
        n_of_employees = User.objects.filter(is_staff=True).count()

        n_of_not_started_votings = Voting.objects.filter(
            start_date__isnull=True, end_date__isnull=True).count()
        n_of_in_progress_votings = Voting.objects.filter(
            start_date__isnull=False, end_date__isnull=True).count()
        n_of_finished_votings = Voting.objects.filter(
            start_date__isnull=False, end_date__isnull=False).count()

        current_user = request.user

        return Response({
            "session": UserAdminSerializer(current_user).data,
            "users": {"total": n_of_users, "active": n_of_active_users, "admins": n_of_admins, "employees": n_of_employees},
            "votings": {"notStarted": n_of_not_started_votings, "inProgress": n_of_in_progress_votings, "finished": n_of_finished_votings}
        })


class VotingAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request):
        votings = Voting.objects.all()
        voting_serializer = AdminVotingGetSerializer(votings, many=True)
        return Response(voting_serializer.data, status=HTTP_200_OK)

    def post(self, request):
        voting_serializer = AdminVotingSerializer(data=request.data)
        is_valid(voting_serializer.is_valid(), voting_serializer.errors)
        auth_url = request.data.get("auth")
        id_users = request.data.get("census")
        auth = Auth.objects.filter(url=auth_url).first()
        if auth is None:
            auth = Auth(name="Auth", url=auth_url, me=True)
            auth.save()
        question = Question(desc=request.data.get('question').get("desc"))
        question.save()
        options = request.data.get('question').get("options")
        for opt in options:
            option = QuestionOption(question=question, option=opt.get(
                "option"), number=opt.get("number"))
            option.save()
        voting = Voting(name=request.data.get("name"), desc=request.data.get("desc"),
                        question=question)
        voting.save()
        voting.auths.add(auth)
        voting_id = voting.id
        if id_users is None:
            users = User.objects.all()
            id_users = [user.id for user in users]
        if len(id_users) > 0:
            for voter_id in id_users:
                census = Census(voting_id=voting_id, voter_id=voter_id)
                census.save()
        return Response({"id": voting_id, "name": voting.name}, status=HTTP_201_CREATED)

    def put(self, request):

        votings_id = request.data.get("idList")
        action = request.data.get('action')
        if not action:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        msg = ''
        st = status.HTTP_200_OK

        if action == 'start':
            votings = Voting.objects.filter(
                id__in=votings_id, start_date__isnull=True)
            if len(votings) > 0:
                for voting in votings:
                    voting.create_pubkey()
                    voting.start_date = timezone.now()
                    voting.save()
                msg = 'Votings started'
            else:
                msg = 'All votings all already started'
                st = status.HTTP_400_BAD_REQUEST
        elif action == 'stop':
            votings = Voting.objects.filter(
                id__in=votings_id, start_date__isnull=False, end_date__isnull=True)
            if len(votings) > 0:
                for voting in votings:
                    voting.end_date = timezone.now()
                    voting.save()
                msg = 'Votings stopped'
            else:
                msg = 'All votings all already stopped or not started'
                st = status.HTTP_400_BAD_REQUEST
        elif action == 'tally':
            votings = Voting.objects.filter(
                id__in=votings_id, start_date__isnull=False, end_date__isnull=False)
            if len(votings) > 0:
                for voting in votings:
                    key = request.COOKIES.get('token', "")
                    voting.tally_votes(key)
                    msg = 'Votings tallied'
            else:
                msg = 'All votings all already tallied, not stopped or not started'
                st = status.HTTP_400_BAD_REQUEST
        else:
            msg = 'Action not found, try with start, stop or tally'
            st = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=st)

    def delete(self, request):
        if request.data.get("idList") is None:
            Voting.objects.all().delete()
            return Response({}, status=HTTP_204_NO_CONTENT)
        else:
            ids = request.data.get("idList")
            is_valid(len(ids) > 0, 'The format of the ids list is not correct')
            Voting.objects.filter(id__in=ids).delete()
            return Response({}, status=HTTP_204_NO_CONTENT)


class VotingsAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request, voting_id):
        votings = get_object_or_404(Voting.objects.filter(id=voting_id))
        voting_serializer = VotingSerializer(votings).data
        return Response(voting_serializer, status=HTTP_200_OK)

    def put(self, request, voting_id):
        voting_serializer = AdminVotingSerializer(data=request.data)
        is_valid(voting_serializer.is_valid(), voting_serializer.errors)
        voting = get_object_or_404(Voting.objects.all().filter(id=voting_id))
        voting.name = request.data.get("name")
        voting.desc = request.data.get("desc")
        auth_url = request.data.get("auth")
        auth = voting.auths.all().first()
        if auth is not None and auth.url != auth_url:
            auth.url = request.data.get("auth")
            auth.save()
        question_request = request.data.get("question")
        voting.question.desc = question_request["desc"]
        options = QuestionOption.objects.all().filter(question__pk=voting.question.id)
        options_request = question_request.get("options")
        tam = max(len(options), len(options_request))
        for i in range(0, tam):
            if i < len(options) and i < len(options_request):
                option = options[i]
                option.number = options_request[i].get("number", option.number)
                option.option = options_request[i].get("option", option.option)
                option.save()
            else:
                if len(options) > len(options_request):
                    option = options[i]
                    option.delete()
                else:
                    opt = QuestionOption(question=voting.question,
                                         number=options_request[i].get(
                                             "number"),
                                         option=options_request[i].get("option"))
                    opt.save()
        voting.question.save()
        voting.save()

        census_request = set(request.data.get("census"))
        census = set(
            [census.voter_id for census in Census.objects.filter(voting_id=voting_id)])
        census_add = census_request - census
        census_delete = census - census_request
        if len(census_add) > 0:
            for voter_id in census_add:
                census = Census(voting_id=voting_id, voter_id=voter_id)
                census.save()
        if len(census_delete) > 0:
            Census.objects.filter(voter_id__in=census_delete).delete()

        return Response({}, status=HTTP_200_OK)

    def delete(self, request, voting_id):
        Voting.objects.all().filter(id=voting_id).delete()
        return Response({}, status=HTTP_204_NO_CONTENT)


class QuestionsAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request):
        questions = Question.objects.all()
        question_serializer = AdminQuestionSerializer(
            questions, many=True).data
        return Response(question_serializer, status=HTTP_200_OK)

    def post(self, request):
        question_serializer = AdminQuestionSerializer(data=request.data)
        is_valid(question_serializer.is_valid(), question_serializer.errors)
        question_serializer.save()
        return Response({}, status=HTTP_201_CREATED)

    def delete(self, request):
        if request.data.get("idList") is None:
            Question.objects.all().delete()
            return Response({}, status=HTTP_204_NO_CONTENT)
        else:
            ids = request.data.get("idList")
            is_valid(len(ids) > 0, 'The format of the ids list is not correct')
            Question.objects.filter(id__in=ids).delete()
            return Response({}, status=HTTP_204_NO_CONTENT)


class QuestionAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request, question_id):
        question = get_object_or_404(Question.objects.filter(id=question_id))
        question_serializer = AdminQuestionSerializer(question).data
        return Response(question_serializer, status=HTTP_200_OK)

    def put(self, request, question_id):
        question = Question.objects.get(id=question_id)
        question_serializer = AdminQuestionSerializer(
            question, data=request.data)
        is_valid(question_serializer.is_valid(), question_serializer.errors)
        question_serializer.save()
        return Response(question_serializer.data, status=HTTP_200_OK)

    def delete(self, request, question_id):
        Question.objects.all().filter(id=question_id).delete()
        return Response({}, status=HTTP_204_NO_CONTENT)


class CensussAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request):
        censuss = Census.objects.all().values()
        return Response(censuss, status=HTTP_200_OK)

    def post(self, request):
        census_serializer = CensusSerializer(data=request.data)
        is_valid(census_serializer.is_valid(), census_serializer.errors)
        census_serializer.save()
        return Response({}, status=HTTP_201_CREATED)

    def delete(self, request):
        if request.data.get("idList") is None:
            Census.objects.all().delete()
            return Response({}, status=HTTP_200_OK)
        else:
            ids = request.get("idList")
            Census.objects.filter(id__in=ids).delete()
            return Response({}, status=HTTP_200_OK)


class CensusAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request, census_id):
        census = get_object_or_404(
            Census.objects.all().values().filter(id=census_id))
        return Response(census, status=HTTP_200_OK)

    def put(self, request, census_id):
        census_serializer = CensusSerializer(data=request.data)
        is_valid(census_serializer.is_valid(), census_serializer.errors)
        census = get_object_or_404(Census.objects.all().filter(id=census_id))
        for key, value in request.data.items():
            setattr(census, key, value)
        census.save()
        return Response({}, status=HTTP_200_OK)

    def delete(self, request, census_id):
        Census.objects.all().filter(id=census_id).delete()
        return Response({}, status=HTTP_204_NO_CONTENT)


class AuthsAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request):
        auths = Auth.objects.all().values()
        return Response(auths, status=HTTP_200_OK)

    def post(self, request):
        auth_serializer = AuthSerializer(data=request.data)
        is_valid(auth_serializer.is_valid(), auth_serializer.errors)
        auth_serializer.save()
        return Response({}, status=HTTP_201_CREATED)

    def delete(self, request):
        if request.data.get("idList") is None:
            Auth.objects.all().delete()
            return Response({}, status=HTTP_204_NO_CONTENT)
        else:
            ids = request.data.get("idList")
            is_valid(len(ids) > 0, 'The ids list can not be empty')
            Auth.objects.filter(id__in=ids).delete()
            return Response({}, status=HTTP_204_NO_CONTENT)


class AuthAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request, auth_id):
        auth = get_object_or_404(
            Auth.objects.all().values().filter(id=auth_id))
        return Response(auth, status=HTTP_200_OK)

    def put(self, request, auth_id):
        auth_serializer = AuthSerializer(data=request.data)
        is_valid(auth_serializer.is_valid(), auth_serializer.errors)
        auth = get_object_or_404(Auth.objects.all().filter(id=auth_id))
        for key, value in request.data.items():
            setattr(auth, key, value)
        auth.save()
        return Response({}, status=HTTP_200_OK)

    def delete(self, request, auth_id):
        Auth.objects.all().filter(id=auth_id).delete()
        return Response({}, status=HTTP_204_NO_CONTENT)


class KeysAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request):
        keys = Key.objects.all().values()
        return Response(keys, status=HTTP_200_OK)

    def post(self, request):
        key_serializer = KeySerializer(data=request.data)
        is_valid(key_serializer.is_valid(), key_serializer.errors)
        key_serializer.save()
        return Response({}, status=HTTP_201_CREATED)

    def delete(self, request):
        if request.data.get("idList") is None:
            Key.objects.all().delete()
            return Response({}, status=HTTP_204_NO_CONTENT)
        else:
            ids = request.data.get("idList")
            is_valid(len(ids) > 0, 'The ids list can not be empty')
            Key.objects.filter(id__in=ids).delete()
            return Response({}, status=HTTP_204_NO_CONTENT)


class KeyAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request, key_id):
        key = get_object_or_404(Key.objects.all().values().filter(id=key_id))
        return Response(key, status=HTTP_200_OK)

    def put(self, request, key_id):
        key_serializer = KeySerializer(data=request.data)
        is_valid(key_serializer.is_valid(), key_serializer.errors)
        keym = get_object_or_404(Key.objects.all().filter(id=key_id))
        for key, value in request.data.items():
            setattr(keym, key, value)
        keym.save()
        return Response({}, status=HTTP_200_OK)

    def delete(self, request, key_id):
        Key.objects.all().filter(id=key_id).delete()
        return Response({}, status=HTTP_204_NO_CONTENT)


class UsersAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request):
        users = User.objects.all()
        user_serializer = UserAdminSerializer(users, many=True).data
        return Response(user_serializer, status=HTTP_200_OK)

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        is_valid(user_serializer.is_valid(), user_serializer.errors)
        fields = request.data
        user = User(username=fields['username'], first_name=fields['first_name'],
                    last_name=fields['last_name'], email=fields['email'], is_staff=False)
        user.set_password(request.data['password'])
        user.save()
        return Response({}, status=HTTP_201_CREATED)

    def delete(self, request):
        if request.data.get("idList") is None:
            User.objects.all().filter(is_superuser=False).delete()
            return Response({}, status=HTTP_200_OK)
        else:
            ids = request.data.get("idList")
            is_valid(len(ids) > 0, 'The ids list can not be empty')
            User.objects.filter(id__in=ids).delete()
            return Response({}, status=HTTP_204_NO_CONTENT)


class UserAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request, user_id):
        user = get_object_or_404(User.objects.filter(id=user_id))
        user_serializer = UserAdminSerializer(user).data
        return Response(user_serializer, status=HTTP_200_OK)

    def put(self, request, user_id):
        user_serializer = UserUpdateSerializer(data=request.data)
        is_valid(user_serializer.is_valid(), user_serializer.errors)
        user = get_object_or_404(User.objects.filter(id=user_id))
        for key, value in request.data.items():
            if value:
                setattr(user, key, value)
        if request.data.get('password'):
            user.set_password(request.data['password'])
        user.save()
        return Response({}, status=HTTP_200_OK)

    def delete(self, request, user_id):
        User.objects.all().filter(is_superuser=False, id=user_id).delete()
        return Response({}, status=HTTP_204_NO_CONTENT)


class LoginAuthAPI(APIView):
    parser_classes = (parsers.FormParser,
                      parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        user_serializer = self.serializer_class(data=request.data,
                                                context={'request': request})
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if not token.user.is_superuser:
            return Response({"error": "Only super user can access here"}, status=HTTP_403_FORBIDDEN)
        response = Response({}, status=HTTP_200_OK)
        response.set_cookie('token', token.key)
        return response


class LogoutAuthAPI(APIView):

    def get(self, request):
        response = Response({}, status=HTTP_200_OK)
        response.delete_cookie('token')
        return response


class UpdateUserStateAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def post(self, request):
        ids = request.data.get("idList")
        state = request.data['state']
        value = request.data['value']
        is_valid(len(ids) > 0, 'The ids list can not be empty')
        is_valid(value == 'True' or value == 'False',
                 'The field value must be True or False')
        res = Response({}, status=HTTP_200_OK)
        if state == 'Active':
            users = User.objects.filter(id__in=ids)
            users.update(is_active=value)
        elif state == 'Staff':
            users = User.objects.filter(id__in=ids)
            users.update(is_staff=value)
        elif state == 'Superuser':
            users = User.objects.filter(id__in=ids)
            users.update(is_superuser=value)
        else:
            res = Response({"result": "The field state must be Active, Staff or Superuser"},
                           status=HTTP_400_BAD_REQUEST)
        return res
