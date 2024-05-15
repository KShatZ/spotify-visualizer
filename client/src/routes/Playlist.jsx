import { useLoaderData } from "react-router-dom";

import Navbar from "../components/nav/Navbar";
import MetaCarousel from "../components/meta-carousel/MetaCarousel";
import SpotifyPlaylistImg from "../components/meta-carousel/items/SpotifyPlaylistImg";
import TracksHeader from "../components/headers/tracks-header/TracksHeader";
import Tracks from "../components/tracks/Tracks";

import spotifyLogo from "../assets/spotify_assets/icon/Spotify_Icon_RGB_Green.png";

export default function Playlist() {

    const playlist = useLoaderData();

    const carouselItems = [
        <SpotifyPlaylistImg key="spotify-playlist-img" img={spotifyLogo} />,
    ];

    return (
        <>
            <Navbar />
            <MetaCarousel items={carouselItems} />
            <div style={{textAlign: "center"}} className="container">
                <h1 id="meta-title">Liked Songs</h1>
                <p id="playlist-duration">5 hours 33 minutes 27 seconds</p>
            </div>
            <TracksHeader />
            <div className="container">
                <p id="playlist-track-count">Total: 1382</p>
            </div>
            <Tracks />
        </>
    )

}