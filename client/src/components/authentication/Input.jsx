import "./styles.css"

export default function Input({ type }) {

    let labelText = "";
    let inputType = "";

    switch (type) {
        case "username":
            labelText = "Username:";
            inputType = "text";
            break;
        
        case "password":
            labelText = "Password:";
            inputType="password"
            break;
        
        default:
            break;
    }

    return (
        <div id="auth-input-group">
            <label htmlFor={ labelText.toLowerCase() }>{ labelText }</label>
            <input 
                required
                className="bg-color txt-color grey-border-2" 
                name={ labelText.toLowerCase() } 
                type={ inputType } 
            />
        </div>
    )
}