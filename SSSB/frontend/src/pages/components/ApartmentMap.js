import * as React from 'react';
import { useEffect, useState, useRef } from 'react';
import { GoogleMap, LoadScript } from '@react-google-maps/api';
import axios from 'axios';

import LoadingBox from './LoadingBox';
import { fetchApartmentInfo, fetchGeocode } from '../../Api'


const containerStyle = {
  width: '100%',
  height: '500px'
};

const GOOGLE_MAPS_API_KEY = "AIzaSyDJCEBjiueduWAhWQrUBa1RvBe5kWRDG9o";
const GOOGLE_MAP_ID = "475d469c6b759722";

export default function ApartmentMap({ object_number }) {
  const [loading, setLoading] = useState(true);
  const [apartmentInfo, setApartmentInfo] = useState({});
  const mapRef = useRef(null);
  const markerRef = useRef(null);

  const [center, setCenter] = useState({ lat: 59.353827, lng: 18.079083 });

  useEffect(() => {
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetchApartmentInfo(object_number);
        if (response.data && response.data.length > 0) {
          setApartmentInfo(response.data[0]);
          try {
            //const map_response = await axios.get(
            //  `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(response.data[0].address)}&key=${GOOGLE_MAPS_API_KEY}`
            //);
            const map_response = await fetchGeocode(response.data[0].address);
            //console.log(map_response.data);
            if (map_response.data && map_response.data.results && map_response.data.results.length > 0) {
              var res = map_response.data.results[0];
              if (res.geometry && res.geometry.location && res.geometry.location.lat && res.geometry.location.lng) {
                // console.log(res.geometry.location);
                setCenter({ lat: res.geometry.location.lat, lng: res.geometry.location.lng });
              }
            } 
          } catch (error) {
            console.error('Error fetching geocoding data:', error);
          }
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();

  }, [object_number]);

  useEffect(() => {
    if (markerRef.current && mapRef.current) {
      markerRef.current.setPosition(center);
      mapRef.current.panTo(center);
      if (apartmentInfo && apartmentInfo.name) {
        markerRef.current.setTitle(apartmentInfo.name);
      }
    }
  }, [center]);

  const handleMapLoad = (map) => {
    mapRef.current = map;

    // Initialize the marker with the initial center
    markerRef.current = new window.google.maps.Marker({
      position: center,
      map,
      title: "Apartment Location",
    });
  };

  return (
    <React.Fragment>
      <LoadingBox loading={loading} sx={{ width: '100%' }}>
        <LoadScript 
          libraries={['marker']}
          version="weekly"
          googleMapsApiKey={GOOGLE_MAPS_API_KEY}
        >
          {center && (
            <GoogleMap
              mapId={GOOGLE_MAP_ID}
              mapContainerStyle={containerStyle}
              center={center}
              zoom={13}
              onLoad={handleMapLoad}
            >
            </GoogleMap>
          )}
        </LoadScript>
      </LoadingBox>
    </React.Fragment>
  );
}
