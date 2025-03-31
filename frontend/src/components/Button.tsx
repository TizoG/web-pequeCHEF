import { Link } from "react-router-dom";

type Props = {
  text: string;
  to?: string;
  onClick?: () => void;
  type?: "button" | "submit";
  className?: string;
};

export function Button({
  text,
  to,
  onClick,
  type = "button",
  className = "",
}: Props) {
  return to ? (
    <Link to={to} className={className}>
      {text}
    </Link>
  ) : (
    <button className={className} type={type} onClick={onClick}>
      {text}
    </button>
  );
}

// TODO: Lo de este boton es una fumada es mas facil poner un simple link
