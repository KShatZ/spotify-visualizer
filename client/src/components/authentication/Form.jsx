import Input from "./Input";
import "./styles.css";

export default function Form({ isLogin }) {

    return (
        <div id="auth-form-container" className="container">
            <form id="auth-form" className="grey-border-2" action="/login" method="POST">

                <h1>{ isLogin ? "Login:":"Register:" }</h1>

                <div id="auth-form-inputs">
                    <Input type="username" />
                    <Input type="password" />
                </div>

                {/* <p id="form-error"></p> */}

                <button type="submit" style={ isLogin ? {}:{width:"65%"} }>{ isLogin ? "Login":"Create Account" }</button>

                { isLogin ? 
                    <div id="auth-redirect">
                        <p>Dont have an account?</p>
                        <a href="/register">Create Account</a>
                    </div>
                    :
                    <div id="auth-redirect">
                        <p>Already have an account?</p>
                        <a href="/login">Login</a>
                    </div>
                }
            </form>
        </div>
       
    )
}