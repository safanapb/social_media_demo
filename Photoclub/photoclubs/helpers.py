def count_increment(like, in_count_obj):
    if like:
        in_count_obj.count += 1
    else:
        if in_count_obj.count >= 1:
            in_count_obj.count -= 1
    in_count_obj.save()
