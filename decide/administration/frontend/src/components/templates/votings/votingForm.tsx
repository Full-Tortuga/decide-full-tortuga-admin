import React from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { Add, Edit } from "@mui/icons-material";

import { votingType } from "types";
import { votingApi } from "api";
import { utils } from "utils";

import { Input } from "components/01-atoms";
import { Severity } from "components/01-atoms/Notification";
import { Modal, ModalPage } from "components/02-molecules";
import { CensusInput, QuestionInput } from ".";

const Component = (props: {
  initialVoting?: votingType.Voting;
  refetch: () => void;
  notify?: (type: Severity, message: string) => void;
}) => {
  const editMode = React.useMemo(
    () => !!props.initialVoting?.id,
    [props.initialVoting]
  );

  const {
    control,
    getValues,
    trigger,
    clearErrors,
    formState: { errors },
    reset,
  } = useForm<votingType.VotingFormFields>({ mode: "onChange" });

  const [sent, setSent] = React.useState(false);

  React.useEffect(() => {
    reset({});
    clearErrors();
    trigger();
    if (props.initialVoting) {
      control._defaultValues = {
        name: props.initialVoting?.name,
        desc: props.initialVoting?.desc,
        census: props.initialVoting?.census,
        question: props.initialVoting?.question,
        auth: props.initialVoting?.auth,
      };
    }
  }, [props.initialVoting, control, reset, clearErrors, trigger]);

  const onSubmitFailed = (e: any) => {
    clearErrors();
    props.notify?.("error", "Submit failed: \n" + e);
  };

  const onSubmitSuccess = () => {
    setSent(!sent);
    props.refetch();
    props.notify?.("success", editMode ? "Voting updated" : "Voting created");
    reset({});
  };

  const onSubmit: SubmitHandler<votingType.VotingFormFields> = (data) => {
    if (Object.keys(errors).length === 0)
      if (editMode && props.initialVoting?.id) {
        votingApi
          .updateVoting(data, props.initialVoting?.id)
          .then(() => onSubmitSuccess())
          .catch((error) => onSubmitFailed(utils.parseErrors(error)));
      } else {
        votingApi
          .createVoting(data)
          .then(() => onSubmitSuccess())
          .catch((error) => onSubmitFailed(utils.parseErrors(error)));
      }
  };

  return (
    <Modal
      onSubmit={() => onSubmit(getValues())}
      title={
        editMode ? "Edit Voting " + props.initialVoting?.name : "New Voting"
      }
      openerIcon={editMode ? <Edit /> : <Add />}
      externalClose={sent}
      pages={[
        <ModalPage description="Indique la información de la Votación">
          <Input.Text
            control={control}
            name="name"
            error={errors.name?.message}
            rules={{ required: true }}
          />
          <Input.Text
            control={control}
            name="desc"
            error={errors.desc?.message}
          />
        </ModalPage>,
        <ModalPage description="Indique la pregunta de la Votación">
          <QuestionInput control={control} />
        </ModalPage>,
        <ModalPage description="Indique el censo de la Votación">
          <CensusInput control={control} />
        </ModalPage>,
        <ModalPage description="Indique la autorización requerida para la Votación">
          <Input.Radio
            control={control}
            name="auth"
            rules={{ required: true }}
            options={[
              {
                label: "Local (localhost:8000)",
                value: `http://localhost:8000`,
              },
              {
                label: `Default (${window.location.host})`,
                value: `http://${window.location.host}`,
              },
            ]}
          />
        </ModalPage>,
      ]}
    />
  );
};

export default Component;
