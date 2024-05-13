import { useContext } from "react";
import { useLoaderData } from "react-router-dom";

import Navbar from "../components/nav/Navbar";
import MetaCarousel from "../components/meta-carousel/MetaCarousel";
import PlaylistHeader from "../components/playlist-header/PlaylistHeader";
import PlaylistList from "../components/playlist-list/PlaylistList";
import { CurrentUser } from "../field_names";


export default function Dashboard() {

    const currentUser = useContext(CurrentUser);
    const userPlaylists = useLoaderData();
    const spotifyDisplayName = currentUser.spotify_profile.display_name;

    return (
        <>
            <Navbar />
            <MetaCarousel titleContent={spotifyDisplayName} />
            <PlaylistHeader />
            <PlaylistList playlists={userPlaylists} />
        </>
    )

}