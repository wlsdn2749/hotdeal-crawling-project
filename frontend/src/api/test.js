import axios from 'axios';

const API_URL = 'http://localhost:3000/items';

export const fetchItems = async (page = 1, limit = 10) => {
    try {
        const response = await axios.get(API_URL, {
            params: { _page: page, _limit: limit }
        });
        return {
            items: response.data,
            total: 100 // 총 아이템 수를 임의로 100으로 설정
        };
    } catch (error) {
        console.error('Error fetching items:', error);
        throw error;
    }
};
