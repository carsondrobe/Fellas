describe('validateForm', () => {
    it('should return false if username is empty', () => {
        document.getElementById = jest.fn(() => ({ value: '' }));
        expect(validateForm()).toBe(false);
        expect(alert).toHaveBeenCalledWith('Please fill in all fields');
    });

    it('should return false if password is empty', () => {
        document.getElementById = jest.fn((id) => ({ value: id === 'username' ? 'testuser' : '' }));
        expect(validateForm()).toBe(false);
        expect(alert).toHaveBeenCalledWith('Please fill in all fields');
    });

    it('should return false if password is less than 8 characters', () => {
        document.getElementById = jest.fn((id) => ({ value: id === 'username' ? 'testuser' : 'short' }));
        expect(validateForm()).toBe(false);
        expect(alert).toHaveBeenCalledWith('Password must be at least 8 characters long');
    });

    it('should return true if both username and password are valid', () => {
        document.getElementById = jest.fn(() => ({ value: 'test' }));
        expect(validateForm()).toBe(true);
    });
});