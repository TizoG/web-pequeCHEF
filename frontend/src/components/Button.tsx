type Props = {
    text: string;
    onClick?: () => void;
    type?: 'button' | 'submit';
    className?: string;
};

export function Button({
    text,
    onClick,
    type = 'button',
    className = '',
}: Props) {
    return (
        <button className={className} type={type} onClick={onClick}>
            {text}
        </button>
    );
}
