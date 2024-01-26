import Header from "../components/authentication/Header";
import Form from "../components/authentication/Form";

export default function Login() {

    return (
    <>
        <Header />
        <Form isLogin={true} />
    </>
    )
}
