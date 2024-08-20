# Name: Kent Tolzmann
# OSU Email: tolzmank@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 08/13/2024
# Description: Optimized HashMap Chaining for collision resolution
#              implementation with several data manipulation methods


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates key/value pair in hash map
        Adds key/value pair in hash map if key doesn't exist in hash map
        """
        self.check_resize_needed()

        # compute element's bucket index
        hash = self._hash_function(key)
        index = hash % self._buckets.length()

        # update or insert new element into hashmap
        ll = self._buckets.get_at_index(index)
        node = ll.contains(key)
        if node is not None:
            node.value = value
        else:
            ll.insert(key, value)
            self._size += 1

    def check_resize_needed(self):
        """
        Checks if the capacity needs to be increased
        Resizes the capacity if needed
        """
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

    def resize_table(self, new_capacity: int) -> None:
        """
        Receives a new capacity for the table
        Changes the capacity of the underlying table
            if new capacity parameter meets requirements
        """
        # validate new capacity parameter
        if new_capacity >= 1:
            if self._is_prime(new_capacity) is False:
                new_capacity = self._next_prime(new_capacity)

            # initiate a new DA with empty Linked Lists
            new_table = DynamicArray()
            for i in range(new_capacity):
                new_table.append(LinkedList())

            # hold old table for now to move values over
            # update pointers
            old_table = self._buckets
            self._buckets = new_table
            self._capacity = new_capacity
            self._size = 0

            # rehash table links
            for i in range(old_table.length()):
                ll = old_table.get_at_index(i)
                if ll.length() != 0:
                    for node in ll:
                        self.put(node.key, node.value)

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        n = self._size
        m = self._capacity
        return n / m

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        count = 0
        for i in range(self._capacity):
            ll = self._buckets.get_at_index(i)
            if ll.length() == 0:
                count += 1
        return count

    def get(self, key: str):
        """
        Receives a key
        Returns the value associated with the given key
        Returns None of key not found
        """
        # compute element's bucket index
        hash = self._hash_function(key)
        index = hash % self._buckets.length()

        # retrieve node from bucket
        ll = self._buckets.get_at_index(index)
        node = ll.contains(key)
        if node is not None:
            return node.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Receives a key
        Returns True if given key is in hash map
        Returns False if key not found
        """
        if self.get(key) is not None:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map
        """
        # compute element's bucket index
        hash = self._hash_function(key)
        index = hash % self._buckets.length()

        # retrieve node from bucket
        ll = self._buckets.get_at_index(index)
        node = ll.contains(key)

        if node is not None:
            ll.remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a new Dynamic Array where each index contains
            tuples of each key/value pair stored in the hash map
        """
        # create new da, iterate through old da to get all key/values
        # append each key/value tuple to new da
        arr = DynamicArray()
        for i in range(self._buckets.length()):
            ll = self._buckets.get_at_index(i)
            for node in ll:
                arr.append((node.key, node.value))
        return arr

    def clear(self) -> None:
        """
        Clears the contents of the hash map
        Capacity remains unchanged
        """
        arr = DynamicArray()
        for i in range(self._capacity):
            arr.append(LinkedList())
        self._buckets = arr
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Receives a Dynamic Array
    Calculates the mode of the values in the Dynamic Array
    Returns a tuple of a new Dynamic Array
        with the modes, and the mode frequency
    """
    freq_high = 0  # initiate current running highest frequency
    mode_arr = DynamicArray()  # initiate current running array of mode values

    # create a hash map of the dynamic array
    map = HashMap()
    for i in range(da.length()):
        key = da.get_at_index(i)
        if map.contains_key(key):
            map.put(key, map.get(key) + 1)
        else:
            map.put(key, 1)

    # iterate through hash map to find highest frequency of values
    keys_values = map.get_keys_and_values()
    for i in range(keys_values.length()):
        key, freq = keys_values.get_at_index(i)
        if freq > freq_high:
            freq_high = freq
            mode_arr = DynamicArray()
            mode_arr.append(key)
        elif freq == freq_high:
            mode_arr.append(key)

    return mode_arr, freq_high



# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")



