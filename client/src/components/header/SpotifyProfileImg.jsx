export default function SpotifyProfileImg({ onTouchStart, onTouchMove, onTouchEnd }) {

    return (

        <div 
            id="spot-img-container" 
            className="carousel-item-container exit-left grey-border-2"
            onTouchStart={ onTouchStart }
            onTouchMove={ onTouchMove }
            onTouchEnd={ onTouchEnd }
        >
            <img src="https://i.scdn.co/image/ab6775700000ee8551711072c1bc64f575929054" alt="Users' Spotify Profile Image" />
        </div>

    )

}
