import { useContext } from "react";

import { CurrentUser } from "../../../field_names";


export default function SpotifyProfileImg({ onTouchStart, onTouchMove, onTouchEnd }) {

    const currentUser = useContext(CurrentUser);
    const spotify_profile_image = currentUser.spotify_profile.profile_image;

    return (

        <div 
            id="spot-img-container" 
            className="carousel-item-container exit-left grey-border-2"
            onTouchStart={onTouchStart}
            onTouchMove={onTouchMove}
            onTouchEnd={onTouchEnd}
        >
            <img src={spotify_profile_image} alt="Users' Spotify Profile Image" />
        </div>

    )

}
