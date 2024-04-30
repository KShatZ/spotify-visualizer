import { Outlet, Navigate, useLoaderData } from "react-router-dom";

export default function Protected() {
    
    const isAuthenticated = useLoaderData();

    return (isAuthenticated ? <Outlet /> : <Navigate to="/login/auth/false" />)
}