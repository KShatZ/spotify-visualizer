import { Link } from "react-router-dom";

import "./styles.css"

export default function TrackCard({ spotifyID, albumCover, name, artists }) {

    return (
        <Link to="#" id="track" >
            <div className="track-album-cover grey-border-3">
                <img src={albumCover}></img>
            </div>

            <div className="track-meta">
                <h3 className="track-name">{name}</h3>
                <p className="track-artists">{artists}</p>
            </div>

            <div className="track-audio-features">
                <p>145</p>
                <p>12B</p>
            </div>
        </Link>
    )
}