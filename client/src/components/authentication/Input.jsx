import { useState } from "react";

import "./styles.css";

export default function Input({ type }) {

    const [ inputText, setInputText ] = useState("");

    function handleChange(e) {

        let inputValue = e.target.value;

        if (type == "password") {
            inputValue = inputValue.replace(/./g, "♫"); // Maybe??
        }

        setInputText(inputValue); 
    }
    

    let labelText = "";

    switch (type) {
        case "username":
            labelText = "Username:";
            break;
        
        case "password":
            labelText = "Password:";
            break;       
        default:
            // This should never happen due to hardcoding the two types
            // -- This may be considered "bad-practice"
            break;
    }

    return (
        <div id="auth-input-group">
            <label htmlFor={ labelText.toLowerCase() }>{ labelText }</label>
            <input 
                className="bg-color txt-color grey-border-2" 
                name={ labelText.toLowerCase() } 
                type="text"
                value={ inputText }
                onChange={ (e) => handleChange(e) }
                required
            />
        </div>
    )
}
