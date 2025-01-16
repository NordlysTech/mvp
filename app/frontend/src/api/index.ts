import axios from 'axios';

const API_URL = 'http://localhost:5000';

export const getMessages = async (queryText: any, isDetailed: any) => {
    try {
        const response = await axios.post(`${API_URL}/query`, {
            query: queryText, // Pass query data
            isDetailed: isDetailed, // Specify whether detailed info is required
        });
        console.log(response)
        return response.data;
    }
    catch (error) {
        console.error('Error fetching messages:', error);
        throw error; // Rethrow error for further handling
    }

}
