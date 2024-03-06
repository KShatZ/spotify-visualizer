export default function SpotifyProfileMeta({ onTouchStart, onTouchMove, onTouchEnd }) {

    return (

        <div 
            id="profile-meta-container" 
            className="carousel-item-container grey-border-2"
            onTouchStart={ onTouchStart }
            onTouchMove={ onTouchMove }
            onTouchEnd={ onTouchEnd }    
        >
            <ul>
                <li>Following: 34</li>
                <li>Followers: 257</li>
            </ul>

            <ul>
                <li>Total Playlists: 81</li>
            </ul>

            <a id="carousel-spot-profile-url" className="grey-border-2" href="google.com" target="_blank">Open Spotify Profile</a>
        </div>

    )

}
