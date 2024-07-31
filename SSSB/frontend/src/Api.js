import axios from 'axios';

const API = axios.create({ baseURL: 'http://localhost:8082/api/' });

export const fetchApartmentAmount = () => API.get('apartment_amount/');

export const fetchItems = () => API.get('items/');
export const createItem = (newItem) => API.post('items/', newItem);
export const updateItem = (id, updatedItem) => API.patch(`items/${id}/`, updatedItem);
export const deleteItem = (id) => API.delete(`items/${id}/`);
