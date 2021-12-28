import React from "react";
import { Add, Edit } from "@mui/icons-material";
import { Input } from "components/01-atoms";
import { Modal, ModalPage } from "components/02-molecules";
import { QuestionInput } from ".";
import { SubmitHandler, useForm } from "react-hook-form";
import { votingType } from "types";

const Component = (props: { initialVoting?: votingType.Voting }) => {
  const editMode = React.useMemo(
    () => !!props.initialVoting?.id,
    [props.initialVoting]
  );

  const {
    control,
    getValues,
    setError,
    formState: { errors },
  } = useForm<votingType.VotingFormFields>({ mode: "onChange" });

  const [sent, setSent] = React.useState(false);

  const onSubmitFailed = (e: any) => {
    console.log("error", e);
    setError("name", { type: "manual", message: "Fake Error" });
  };

  const onSubmit: SubmitHandler<votingType.VotingFormFields> = (data) => {
    console.log("submit:", data);
    setSent(true);

    onSubmitFailed("not failed");
  };

  return (
    <Modal
      onSubmit={() => onSubmit(getValues())}
      title={editMode ? "Edit Voting" : "New Voting"}
      openerIcon={editMode ? <Edit /> : <Add />}
      externalClose={sent}
      pages={[
        <ModalPage description="Indique la información de la Votación">
          <Input.Text
            control={control}
            name="name"
            error={errors.name?.message}
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
        <ModalPage
          description="Indique el censo de la Votación
         (si no selecciona ningún usuario, todos serán añadidos)"
        >
          <span>
            {/* TODO: <CensusInput control={control} /> */}
            Todo: Census Input
          </span>
        </ModalPage>,
        <ModalPage description="Indique la autorización requerida para la Votación">
          <Input.Radio
            control={control}
            name="auth"
            options={[
              {
                label: "Local (localhost:8000)",
                value: `http//localhost:8000`,
              },
              {
                label: `Default (${window.location.host})`,
                value: `http//${window.location.host}`,
              },
            ]}
          />
        </ModalPage>,
      ]}
    />
  );
};

export default Component;
