import { Outlet, Navigate, useLoaderData } from "react-router-dom";

import { CurrentUser } from "../field_names";


export default function Protected() {
    
    const currentUser = useLoaderData();
    
    if (!currentUser) {
        return <Navigate to="/login/auth/false" />
    }

    return (
        <CurrentUser.Provider value={currentUser}>
            <Outlet />
        </CurrentUser.Provider>
    );
}