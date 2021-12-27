export type User = {
  id?: number;
  email: string;
  password?: string;
  first_name: string;
  last_name: string;
  username: string;
  is_active?: boolean;
  is_staff?: boolean;
  is_superuser?: boolean;
};

export type UserFormFields = {
  username: string;
  password: string;
  first_name: string;
  last_name: string;
  email: string;
};
