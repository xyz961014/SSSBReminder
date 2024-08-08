import axios from 'axios';

const API = axios.create({ baseURL: 'http://localhost:8082/' });

export const fetchRegions = () => API.get('get_regions');
export const fetchTypes = () => API.get('get_types');
export const fetchSpaceRange = () => API.get('get_space_range');
export const fetchRentRange = () => API.get('get_rent_range');
export const fetchFloorRange = () => API.get('get_floor_range');
export const fetchCreditRange = () => API.get('get_credit_range');

export const fetchFilteredApartments = (filterDict) => API.post('get_filtered_apartments', filterDict);

export const fetchApartmentInfo = (object_number) => API.get(`api/apartment_info/?object_number=${object_number}`);
export const fetchApartmentStatus = (object_number) => API.get(`api/apartment_status/?object_number=${object_number}`);

export const fetchItems = () => API.get('items/');
export const createItem = (newItem) => API.post('items/', newItem);
export const updateItem = (id, updatedItem) => API.patch(`items/${id}/`, updatedItem);
export const deleteItem = (id) => API.delete(`items/${id}/`);
