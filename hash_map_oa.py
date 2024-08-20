# Name: Kent Tolzmann
# OSU Email: tolzmank@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 08/13/2024
# Description: Optimized HashMap Open Addressing implementation
#              with several data manipulation methods

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Receives a key/value pair
        Updates the value for key in the hash map
        Adds the key/value pair if not found in hash map
        """
        self.check_resize_table()

        # check if key already exists, update value
        hash_entry = self.get_hash_entry(key)
        if hash_entry is not None:
            hash_entry.value = value
        else:
            # compute element's bucket index
            hash = self._hash_function(key)
            i = hash % self._capacity
            i_init = i
            m = self._capacity
            j = 0

            # probe quadratically for empty or tombstone
            new_hash_entry = HashEntry(key, value)
            while self._buckets.get_at_index(i) is not None:
                hash_entry = self._buckets.get_at_index(i)
                if hash_entry.is_tombstone is True:
                    self._buckets.set_at_index(i, new_hash_entry)
                    self._size += 1
                    return
                # increment index
                j += 1
                i = (i_init + j ** 2) % m

            self._buckets.set_at_index(i, new_hash_entry)
            self._size += 1

    def check_resize_table(self):
        """
        Checks if the capacity needs to be increased
        Resizes the capacity if needed
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

    def resize_table(self, new_capacity: int) -> None:
        """
        Receives a new capacity for the table
        Changes the capacity of the underlying table
            if new capacity parameters meets requirements
        """
        # validate new capacity parameter
        if new_capacity > self.get_size():
            if self._is_prime(new_capacity) is False:
                new_capacity = self._next_prime(new_capacity)

            # initiate a new Dynamic Array with new capacity
            new_table = DynamicArray()
            for i in range(new_capacity):
                new_table.append(None)

            # hold old table for now to move values over
            # update pointers to new table
            old_table = self._buckets
            self._buckets = new_table
            self._capacity = new_capacity
            self._size = 0

            # rehash table elements
            for i in range(old_table.length()):
                hash_entry = old_table.get_at_index(i)
                if hash_entry is not None:
                    self.put(hash_entry.key, hash_entry.value)

                    # check if the hash entry added was a tombstone
                    # set hash entry added into new table as a tombstone
                    if hash_entry.is_tombstone is True:
                        self.get_hash_entry(hash_entry.key).is_tombstone = True
                        self._size -= 1

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        n = self.get_size()
        m = self.get_capacity()
        return n / m

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        return self._capacity - self._size

    def get_hash_entry(self, key):
        """
        Receives a key for a hash entry
        Returns the hash entry object for that hash entry if found
        Returns None if not found
        """
        # compute element's bucket index
        hash = self._hash_function(key)
        i = hash % self._capacity
        i_init = i
        m = self._capacity
        j = 0

        # search for hash entry
        while self._buckets.get_at_index(i) is not None:
            hash_entry = self._buckets.get_at_index(i)
            if hash_entry.is_tombstone is False:
                if hash_entry.key == key:
                    return hash_entry
            # increment index
            j += 1
            i = (i_init + j ** 2) % m
        return None

    def get(self, key: str) -> object:
        """
        Receives a key for a hash entry
        Returns the value for that hash entry if found
        Returns None if not found
        """
        # compute element's bucket index
        hash = self._hash_function(key)
        i = hash % self._capacity
        i_init = i
        m = self._capacity
        j = 0

        # search for key
        while self._buckets.get_at_index(i) is not None:
            hash_entry = self._buckets.get_at_index(i)
            if hash_entry.is_tombstone is False:
                if hash_entry.key == key:
                    return hash_entry.value

            # increment index
            j += 1
            i = (i_init + j ** 2) % m
        return None

    def contains_key(self, key: str) -> bool:
        """
        Receives a key for a hash entry
        Returns True if found in the hash map
        Returns False if not found
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
        i = hash % self._capacity
        i_init = i
        m = self._capacity
        j = 0

        # search for key
        while self._buckets.get_at_index(i) is not None:
            hash_entry = self._buckets.get_at_index(i)
            if hash_entry.is_tombstone is False:
                if hash_entry.key == key:
                    hash_entry.is_tombstone = True
                    self._size -= 1
                    return
            # increment index
            j += 1
            i = (i_init + j ** 2) % m

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a new Dynamic Array where each index contains
            tuples of each key/value pair stored in the hash map
        """
        arr = DynamicArray()
        for i in range(self._buckets.length()):
            hash_entry = self._buckets.get_at_index(i)
            if hash_entry is not None and hash_entry.is_tombstone is False:
                arr.append((hash_entry.key, hash_entry.value))
        return arr

    def clear(self) -> None:
        """
        Clears the contents of the hash map
        Capacity remains unchanged
        """
        arr = DynamicArray()
        for i in range(self._capacity):
            arr.append(None)
        self._buckets = arr
        self._size = 0

    def __iter__(self):
        """
        Iterator to enable the hash map to iterate across itself
        """
        # initialize variable to track iterator progress through hashmap
        self._index = 0
        return self

    def __next__(self):
        """
        Returns the next item in the hash map,
            based on current location of the iterator
        """
        # stops at end of array
        while self._index < self.get_capacity():

            # retrieve entry, increment, and return only if active item
            hash_entry = self._buckets.get_at_index(self._index)
            self._index += 1
            if hash_entry is not None and hash_entry.is_tombstone is False:
                return hash_entry

        raise StopIteration


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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

# -------------------------------------------
