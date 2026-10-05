import Keyboard from "react-simple-keyboard";
import "react-simple-keyboard/build/css/index.css";
import { useState } from "react";

type AACKeyboardProps = {
  onInput: (input: string) => void;
}

export default function AACKeyboard(props: AACKeyboardProps) {

  const [keyboardInput, setKeyBoardInput] = useState<string>("")

  const onChange = (input: string) => {
      props.onInput(input)
      setKeyBoardInput(input);
    };

  return (
    <div className="w-full rounded-2xl bg-white p-3 font-aac">
      <div className="relative flex flex-row items-center w-full my-1">
        <h1 className="font-semibold text-2xl mx-3 my-2">Type a topic:</h1>
        <div className="absolute left-1/2 -translate-x-1/2 w-80 h-12 bg-white border-2 border-gray-300 rounded-xl flex items-center justify-center px-4 shadow-inner">
          <span className="font-semibold text-2xl whitespace-nowrap overflow-hidden truncate">
            {keyboardInput}
          </span>
        </div>
      </div>

      <Keyboard
        onChange={onChange}
        theme="hg-theme-default aac-keyboard"
        layout={{
            default: [
            "1 2 3 4 5 6 7 8 9 0",
            "q w e r t y u i o p",
            "a s d f g h j k l",
            "z x c v b n m {bksp}",
            ],
        }}
        display={{
            "{bksp}": "⌫",
        }}
      />
    </div>
  );
}