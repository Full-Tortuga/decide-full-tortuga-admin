import TextInput from "./Text/TextInput";
import SecretInput from "./Secret/SecretInput";

export type FieldProps = {
  name: string;
  control: any;
  error?: string;
};

export type InputProps = FieldProps & {
  type?: "text" | "password";
};

export const FormItem = { TextInput, SecretInput };
