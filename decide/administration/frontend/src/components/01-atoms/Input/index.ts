import Text from "./Text/TextInput";
import Secret from "./Secret/SecretInput";
import Radio from "./Radio/RadioInput";

export type FieldProps = {
  name: string;
  control: any;
  error?: string;
  rules?: any;
};

export type RadioOption = {
  label: string;
  value: string;
};

export type RadioProps = FieldProps & {
  options: RadioOption[];
};

export type InputProps = FieldProps & {
  type?: "text" | "password";
  useFormLabel?: boolean;
};

export const Input = { Text, Secret, Radio };
