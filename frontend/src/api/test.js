import axios from 'axios';

// 실제에선 환경변수에 저장해서 사용할 것
const API_URL = 'http://localhost:3000/items';

export const fetchItems = async () => {
    try {
        const response = await axios.get(API_URL);
        return response.data;
    } catch (error) {
        console.error('Error fetching items:', error);
        throw error;
    }
};