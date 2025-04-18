import axios from 'axios';

export const baseURL = "https://sssbreminder.xyzs.app/";
// export const baseURL = "http://localhost:8082";
const API = axios.create({ baseURL: baseURL });

export const fetchRegions = () => API.get('get_regions');
export const fetchTypes = () => API.get('get_types');
export const fetchSpaceRange = () => API.get('get_space_range');
export const fetchRentRange = () => API.get('get_rent_range');
export const fetchFloorRange = () => API.get('get_floor_range');
export const fetchCreditRange = () => API.get('get_credit_range');

export const fetchFilteredApartments = (filterDict) => API.post('get_filtered_apartments', filterDict);
// export const fetchApartmentPdf = (object_number, drawing_type) => API.get(`get_drawing?object_number=${object_number}&drawing_type=${drawing_type}`);
export const fetchGeocode = (address) => API.get(`get_geocode?address=${encodeURIComponent(address)}`);

export const createFilter = (filterDict) => API.post('api/personal_filter/', filterDict);
export const editFilter = (filterDict) => API.post('edit_personal_filter', {"filter_data": filterDict});

export const fetchApartmentInfo = (object_number, valid_from) => API.get(`api/apartment_info/?object_number=${object_number}&valid_from=${valid_from}`);
export const fetchApartmentStatus = (object_number, valid_from) => API.get(`api/apartment_status/?object_number=${object_number}&valid_from=${valid_from}`);
export const fetchFilterData = (filterId) => API.get(`api/personal_filter/?_id=${filterId}`);
export const unsubscribeFilter = (filterId) => API.get(`unsubscribe_filter?filter_id=${filterId}`);


export const fetchItems = () => API.get('items/');
export const createItem = (newItem) => API.post('items/', newItem);
export const updateItem = (id, updatedItem) => API.patch(`items/${id}/`, updatedItem);
export const deleteItem = (id) => API.delete(`items/${id}/`);
