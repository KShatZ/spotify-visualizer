import Carousel from "./Carousel";
import SpotifyProfileImg from "./SpotifyProfileImg";
import SpotifyProfileMeta from "./SpotifyProfileMeta";

import "./styles.css";


export default function MetaCarousel({ titleContent, duration }) {
    
    const carouselItems = [
        <SpotifyProfileImg key="spotify-profile-image" />,
        <SpotifyProfileMeta key="spotify-profile-meta" />,
    ]

    return (
        <>
            <Carousel items={carouselItems} />

            <div style={{textAlign: "center"}} className="container">
                <h1 id="meta-title">{titleContent}</h1>

                { duration && <p id="playlist-duration">{duration}</p> }
            </div>
        </>
    )
}
