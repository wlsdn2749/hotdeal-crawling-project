import axios from 'axios';

const API_URL = 'http://tools.gyu.be:8000/hotdeal';

export const fetchItems = async (page = 1, limit = 10) => {
    try {
        const response = await axios.get(API_URL, {
            params: { page: page, count: limit }
        });
        return {
            items: response.data,
            total: 200 // 총 아이템 수를 임의로 200으로 설정

        };
    } catch (error) {
        console.error('Error fetching items:', error);
        throw error;
    }
};

//상세 페이지
//사이트(크롤링한 사이트)랑 URL(게시글의 원래 URL)를 파라미터로?
export const detailItem = async (site, url) => {
    try {
        const response = await axios.get(API_URL, {
            params: { site: site, url: url }
        });
        return {
            item: response.data,
        };
    } catch (error) {
        console.error('Error fetching item:', error);
        throw error;
    }
};