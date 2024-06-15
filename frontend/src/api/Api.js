import axios from 'axios';
import qs from 'qs';  // qs 라이브러리 임포트

const API_URL = 'http://tools.gyu.be:8000/hotdeal';

export const fetchItems = async (page = 1, limit = 10) => {
    try {
        const response = await axios.get(API_URL, {
            params: { page, count: limit }
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

// 상세 페이지
// 사이트(크롤링한 사이트)와 URL(게시글의 원래 URL)를 파라미터로
export const detailItem = async (site, url) => {
    try {
        const response = await axios.get(`${API_URL}/detail`, {
            params: { site, url }
        });
        return {
            item: response.data,
        };
    } catch (error) {
        console.error('Error fetching item:', error);
        throw error;
    }
};

// 카테고리로 필터링된 아이템을 가져오는 함수 추가
export const fetchItemsByCategories = async (page = 1, limit = 10, categories = []) => {
    console.log('넘겨받은 카테고리', categories); // 정상
    if (categories.length === 0) {
        return await fetchItems(page, limit);
    }

    try {
        const response = await axios.get(API_URL, {
            params: {
                page,
                count: limit,
                categories
            },
            paramsSerializer: params => qs.stringify(params, { arrayFormat: 'repeat' })  // qs 사용
        });
        return {
            items: response.data,
            total: 200,
        };
    } catch (error) {
        console.error('Error fetching items by categories:', error);
        throw error;
    }
};
