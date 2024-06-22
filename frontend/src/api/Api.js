import axios from 'axios';
import qs from 'qs';  // qs 라이브러리 사용

const API_URL = 'http://tools.gyu.be:8000/hotdeal';

export const fetchItems = async (page = 1, limit = 10, order = 'desc') => {
    try {
        const response = await axios.get(API_URL, {
            params: { page, count: limit, order }
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

// 카테고리 및 정렬 방식으로 필터링된 아이템을 가져오는 함수 추가
export const fetchItemsByCategories = async (page = 1, limit = 10, categories = [], order = 'desc', sites = []) => {
    if (categories.length === 0 && sites.length === 0) {
        return await fetchItems(page, limit, order);
    }

    try {
        const response = await axios.get(API_URL, {
            params: {
                page,
                count: limit,
                categories,
                sites,
                order
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

// 검색어로 필터링된 아이템을 가져오는 함수 추가
export const searchItems = async (page = 1, limit = 10, searchQuery = '', searchMode = 'title', order = 'desc') => {
    console.log('검색 구분', searchMode);
    console.log('검색한 단어', searchQuery);
    try {
        const response = await axios.get(`${API_URL}/search`, {
            params: {
                page,
                count: limit,
                search_mode: searchMode,
                search_query: searchQuery,
                order
            }
        });
        return {
            items: response.data,
            total: 200, // 총 아이템 수를 임의로 200으로 설정
        };
    } catch (error) {
        console.error('Error searching items:', error);
        throw error;
    }
};
