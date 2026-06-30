# msgs/echo_msgs.py
import time

def format_twist(msg):
    """Formatter khusus untuk tipe data Twist"""
    lines = [
        f"  ↳ Linear",
        f"      X: {msg.linear.x:>5.2f}",
        f"      Y: {msg.linear.y:>5.2f}",
        f"      Z: {msg.linear.z:>5.2f}",
        f"  ↳ Angular", 
        f"      X: {msg.angular.x:>5.2f}",
        f"      Y: {msg.angular.y:>5.2f}",
        f"      Z: {msg.angular.z:>5.2f}"
    ]
    return "\n".join(lines)

def format_spatial(msg):
    """Formatter untuk Vector3 atau Point"""
    lines = [
        f"  ↳ X: {msg.x:.2f}",
        f"    Y: {msg.y:.2f}",
        f"    Z: {msg.z:.2f}"
    ]
    return "\n".join(lines)

def format_standard(msg):
    """Formatter untuk tipe data standar (Int32, String, dll)"""
    return f"  ↳ {msg.data}"

def format_fallback(msg):
    """Formatter cadangan jika tipe data tidak dikenal"""
    if hasattr(msg, '__dict__'):
        return f"  ↳ Raw Dict: {msg.__dict__}"
    return f"  ↳ Raw Data: {msg}"

def get_formatted_string(msg, topic_name: str, msg_type_name: str) -> str:
    """
    Fungsi jangkar dengan kustomisasi template header terpusat.
    """
    if hasattr(msg, 'linear') and hasattr(msg, 'angular'):
        content = format_twist(msg)
    elif hasattr(msg, 'x') and hasattr(msg, 'y') and hasattr(msg, 'z'):
        content = format_spatial(msg)
    elif hasattr(msg, 'data'):
        content = format_standard(msg)
    else:
        content = format_fallback(msg)

    if hasattr(msg, 'timestamp') and msg.timestamp and msg.timestamp > 0:
        waktu_lokal = time.strftime('%H:%M:%S', time.localtime(msg.timestamp))
        milidetik = int((msg.timestamp - int(msg.timestamp)) * 1000)
        str_time = f"{waktu_lokal}.{milidetik:03d}"
    else:
        str_time = "-"

    template = [
        "==================================",
        f"topic : {topic_name}",
        f"type  : {msg_type_name}",
        f"timestamp : {str_time}",
        "==================================",
        content,
        ""
    ]
    
    return "\n".join(template)