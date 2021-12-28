import React from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { userType, votationType } from "types";
import { ModalPage, Modal } from "components/02-molecules";
import { Add, Edit } from "@mui/icons-material";
import { FormItem } from "components/01-atoms/Input";

const Component = (props: { initialVotation?: votationType.Votation }) => {
  const {
    control,
    getValues,
    setError,
    formState: { errors },
  } = useForm<{ name: string; name2: string; description: string; question: string; census: string; auth: string;}>({
    defaultValues: { name: props.initialVotation?.name || "", description: props.initialVotation?.description || "",
                     question: props.initialVotation?.question || "", census: props.initialVotation?.census || "",
                     auth: props.initialVotation?.auth || ""},
  });

  const [sent, setSent] = React.useState(false);

  const onSubmitFailed = (e: any) => {
    console.log("error", e);
    setError("name", { type: "manual", message: "Fake Error" });
    setError("description", { type: "manual", message: "Fake Error" });
    setError("question", { type: "manual", message: "Fake Error" });
    setError("census", { type: "manual", message: "Fake Error" });
    setError("auth", { type: "manual", message: "Fake Error" });

  };

  const onSubmit: SubmitHandler<{ name: string; name2: string }> = (
    data
  ) => {
    //todo: if initialUser empty then call create new user
    //todo: if initialUser is not empty, then call update
    console.log("submit:", data);
    //Todo: call api and create user,
    //Todo: if created then close modal if not, call onSubmitFailed
    setSent(true);

    onSubmitFailed("not failed");
  };

  return (
    <Modal
      onSubmit={() => onSubmit(getValues())}
      title="New Votation"
      openerIcon={props.initialVotation ? <Edit /> : <Add />}
      externalClose={sent}
      pages={[
        <ModalPage description="Indique la información de la Votación">
          <FormItem.TextInput
            control={control}
            name="Name"
            error={errors.name?.message}
          />
        </ModalPage>,
        <ModalPage description="Indique la información de la Votación">
        <FormItem.TextInput
          control={control}
          name="Question"
          error={errors.question?.message}
        />
        
      </ModalPage>,
      <ModalPage description="Indique la información de la Votación">
      <FormItem.TextInput
        control={control}
        name="Census"
        error={errors.census?.message}
      />
      
    </ModalPage>,
    <ModalPage description="Indique la información de la Votación">
    <FormItem.TextInput
      control={control}
      name="Auth"
      error={errors.auth?.message}
    />
    
  </ModalPage>,
      ]}
    />
  );
};

export default Component;