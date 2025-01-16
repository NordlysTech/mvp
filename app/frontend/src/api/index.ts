import axios from 'axios';

const API_URL = 'http://localhost:5008';

export const getMessages = async (queryText) => {
    try {
        const response = await axios.post(`${API_URL}/query`, {
            query: queryText, // Pass query data
        });
        console.log(response)
        return response.data;
    }
    catch (error) {
        console.error('Error fetching messages:', error);
        throw error; // Rethrow error for further handling
    }

}
