import { useState, useEffect, useRef } from "react";

import DropdownMenu from "./DropdownMenu";
import DropdownToggle from "./DropdownToggle";
import "./styles.css";

export default function Navbar() {

    // Depending on re-render cost in the future (nav component), this might need to be a ref.
    const [ isVisible, setIsVisible ] = useState(false);
    const menuElement = useRef(null);


    function handleToggleClick() {
        setIsVisible(!isVisible);   
    }

    function handleDropdownScroll(event) {
        event.preventDefault();
    }

    function handleDropdownClose(event) {
        const clickedElement = event.target;
        const menuLinks = Array.from(menuElement.current.children);

        if (!menuLinks.includes(clickedElement)) {
            setIsVisible(false);
        } 
    }

    useEffect(() => {
        
        if (isVisible) {
            document.addEventListener("scroll", handleDropdownScroll);
            document.addEventListener("click", handleDropdownClose);
        }

        return (() => {
            document.removeEventListener("scroll", handleDropdownScroll);
            document.removeEventListener("click", handleDropdownClose);
        });

    }, [isVisible]);


    return (
        <nav>
            <div id="navbar-container" className="bg-color">
                <div id="navbar" className="container">
                    <a href="/">Spotify Visualizer</a>   { /* Todo: Nav Component */ }
                    <DropdownToggle 
                        user="kshats" 
                        onClick={ handleToggleClick }
                        isOpen={ isVisible } 
                    />
                </div>
            </div>
            <DropdownMenu isVisible={ isVisible } ref={ menuElement } />
        </nav>
    )
}

