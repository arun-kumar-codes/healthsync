import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Settings = () => {
    const [userData, setUserData] = useState({
        username: '',
        email: '',
        dataSharing: false,
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await axios.get('/api/user/settings');
                setUserData(response.data);
            } catch (err) {
                setError('Failed to load user data');
            } finally {
                setLoading(false);
            }
        };
        fetchUserData();
    }, []);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setUserData({
            ...userData,
            [name]: type === 'checkbox' ? checked : value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.put('/api/user/settings', userData);
            alert('Settings updated successfully');
        } catch (err) {
            setError('Failed to update settings');
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div>
            <h1>User Settings</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>
                        Username:
                        <input
                            type="text"
                            name="username"
                            value={userData.username}
                            onChange={handleChange}
                            required
                        />
                    </label>
                </div>
                <div>
                    <label>
                        Email:
                        <input
                            type="email"
                            name="email"
                            value={userData.email}
                            onChange={handleChange}
                            required
                        />
                    </label>
                </div>
                <div>
                    <label>
                        Data Sharing:
                        <input
                            type="checkbox"
                            name="dataSharing"
                            checked={userData.dataSharing}
                            onChange={handleChange}
                        />
                    </label>
                </div>
                <button type="submit">Save Changes</button>
            </form>
        </div>
    );
};

export default Settings;