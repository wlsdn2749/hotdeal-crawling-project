// api.js
import axios from 'axios';
import qs from 'qs';  // qs 라이브러리 사용

const API_URL = 'http://tools.gyu.be:8000/hotdeal';

// 아이템 목록을 가져오는 함수
export const fetchItems = async (page = 1, limit = 20, order = 'desc') => {
    try {
        const response = await axios.get(API_URL, {
            params: { page, count: limit, order }
        });
        // 응답 헤더에서 총 개수 가져오기
        const totalCount = response.headers['x-total-count'];
        // console.log('헤더 열어보기', response.headers);
        // console.log(totalCount);
        return {
            items: response.data,
            total: totalCount ? parseInt(totalCount, 10) : 200  // 총 아이템 수를 헤더에서 가져오거나 기본값 200으로 설정
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
        if (error.response && error.response.status === 404) {
            // 404 에러가 발생하면 새로운 창을 열어 매개변수 url 경로로 이동시킴
            window.open(url, '_blank');
            return; // 추가적인 처리가 없도록 리턴
        }
        console.error('Error fetching item:', error);
        throw error;
    }
};

// 카테고리 및 정렬 방식으로 필터링된 아이템을 가져오는 함수
export const fetchItemsByCategories = async (page = 1, limit = 20, categories = [], order = 'desc', sites = []) => {

    if (categories.length === 0 && sites.length === 0) {
        console.log("test1")
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
        // 응답 헤더에서 총 개수 가져오기
        const totalCount = response.headers['x-total-count'];
        console.log("test2")
        return {
            items: response.data,
            total: totalCount ? parseInt(totalCount, 10) : 200,  // 총 아이템 수를 헤더에서 가져오거나 기본값 200으로 설정
        };
    } catch (error) {
        console.log("test3")
        console.error('Error fetching items by categories:', error);
        throw error;
    }
};

// 검색어로 필터링된 아이템을 가져오는 함수
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
        // 응답 헤더에서 총 개수 가져오기
        const totalCount = response.headers['x-total-count'];
        return {
            items: response.data,
            total: totalCount ? parseInt(totalCount, 10) : 200,  // 총 아이템 수를 헤더에서 가져오거나 기본값 200으로 설정
        };
    } catch (error) {
        console.error('Error searching items:', error);
        throw error;
    }
};
