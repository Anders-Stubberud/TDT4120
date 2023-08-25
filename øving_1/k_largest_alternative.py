

def k_largest_alternative(arr, k):
    def merge_sort_reverse(arr):
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        
        left_half = merge_sort_reverse(left_half)
        right_half = merge_sort_reverse(right_half)
        
        return merge(left_half, right_half)

    def merge(left, right):
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] > right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    liste = merge_sort_reverse(arr)
    res = 0
    for i in range(k):
        res += liste[i]
    return res
    
print(k_largest_alternative([5,7,9,2,3,5], 2))