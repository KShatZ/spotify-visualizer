import { Link } from "react-router-dom";

import "./styles.css"

export default function TrackCard({ spotifyID, albumCover, name, artists }) {

    return (
        <Link to="#" id="track" >
            <div className="track-album-cover grey-border-3">
                <img src={albumCover}></img>
            </div>

            <div className="track-meta">
                <h3 className="track-name pointer">{name}</h3>
                <p className="track-artists pointer">{artists}</p>
            </div>

            <div className="track-audio-features">
                <p className="pointer">145</p>
                <p className="pointer">12B</p>
            </div>
        </Link>
    )
}