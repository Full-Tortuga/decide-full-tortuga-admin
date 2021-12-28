import TextInput from "./Text/TextInput";
import SecretInput from "./Secret/SecretInput";

export type FieldProps = {
  name: string;
  control: any;
  error?: string;
  rules?: any;
};

export type InputProps = FieldProps & {
  type?: "text" | "password";
  useFormLabel?: boolean;
};

export const FormItem = { TextInput, SecretInput };
