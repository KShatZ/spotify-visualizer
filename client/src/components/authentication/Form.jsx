import { useState } from "react";
import { Link } from "react-router-dom";

import "./styles.css";

export default function Form({ isLogin }) {

    const [ username, setUsername ] = useState("");
    const [ password, setPassword ] = useState("");

    function handleInput(event) {
        const inputName = event.target.name;
        let inputValue = event.target.value;

        switch (inputName) {
            case "username":
                setUsername(inputValue);
                break;
            case "password":
                inputValue = inputValue.replace(/./g, "♫"); // Maybe??
                setPassword(inputValue);
                break;
            default:
                break;
        }
    }


    async function handleSubmit(event) {
        event.preventDefault();

        // Todo: Better input validation
        if (username.length == 0 || password.length == 0) {
            console.log("The username and password fields cannot be empty");
            return;
        }

        const userCredentials = {
            "username": username,
            "password": password
        }

        const endpoint = isLogin ? "login" : "register"; 

        // Todo: Create own request interface
        const response = await fetch(`http://127.0.0.1:5000/${endpoint}`, {
            method: "POST",
            body: JSON.stringify(userCredentials),
            headers: {
                "Content-Type": "application/json"
            }
        });
        console.log("The RESPONSE: ", response);
            
        const responseBody = await response.json();
        console.log("Response BODY: ", responseBody);
    }


    return (
        <div id="auth-form-container" className="container">
            <form id="auth-form" className="grey-border-2" onSubmit={ handleSubmit }>

                <h1>{ isLogin ? "Login:":"Register:" }</h1>

                <div id="auth-form-inputs">
                    <div id="auth-input-group">
                        <label htmlFor="username">Username:</label>
                        <input className="bg-color txt-color grey-border-2"
                            id="username"
                            name="username"
                            value={ username }
                            type="text"
                            onChange={ handleInput }
                        />
                    </div>

                    <div id="auth-input-group">
                        <label htmlFor="password">Password:</label>
                        <input className="bg-color txt-color grey-border-2"
                            id="password"
                            name="password"
                            value={ password }
                            type="text"
                            onChange={ handleInput }
                        />
                    </div>
                </div>

                {/* <p id="form-error"></p> */}

                <button type="submit" style={ isLogin ? {}:{width:"65%"} }>{ isLogin ? "Login":"Create Account" }</button>

                { isLogin ? 
                    <div id="auth-redirect">
                        <p>Dont have an account?</p>
                        <Link to="/register">Create Account</Link>
                    </div>
                    :
                    <div id="auth-redirect">
                        <p>Already have an account?</p>
                        <Link to="/login">Login</Link>
                    </div>
                }
            </form>
        </div>
       
    )
}