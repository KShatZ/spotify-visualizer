import HeaderCarousel from "./HeaderCarousel";
import SpotifyProfileImg from "./SpotifyProfileImg";
import SpotifyProfileMeta from "./SpotifyProfileMeta";

import "./styles.css";


export default function Header({ titleContent, duration }) {
    
    const carouselItems = [
        <SpotifyProfileImg key="spotify-profile-image" />,
        <SpotifyProfileMeta key="spotify-profile-meta" />,
    ]

    return (
        <>
            <HeaderCarousel items={ carouselItems } />

            <div style={{textAlign: "center"}} className="container">
                <h1 id="header-title">{ titleContent }</h1>

                { duration && <p id="playlist-duration">{ duration }</p> }
            </div>
        </>
    )
}
