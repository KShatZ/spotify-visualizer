import TrackCard from "./TrackCard";

import tracksData from "./tracks.json";
import "./styles.css"

export default function Tracks({ tracks }) {

    return (

        <div id="tracks-container" className="container">
            {
                tracksData.map((track) => {
                    return (
                        <TrackCard 
                            key={track._id} 
                            albumCover={track.track.album.images[0].url}
                            name={track.track.name}
                            artists={track.track.artists[0].name}
                        />
                    )
                })
            }
        </div>
    )

}