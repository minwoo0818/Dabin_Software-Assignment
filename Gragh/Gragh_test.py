import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)
y = np.sin(x) + 0.5 * np.sin(100)  # 변화가 급한 구간 포함

# 완화 전: 기울기 그대로 사용
def raw_error_bounds(x, y, base_error=0.3, slope_factor=0.5):
    dy = np.diff(y)
    dx = np.diff(x)
    raw_slopes = np.abs(dy / dx)
    raw_slopes = np.append(raw_slopes, raw_slopes[-1])
    total_error = base_error + slope_factor * raw_slopes
    return y - total_error, y + total_error

# 완화 후: tanh로 부드럽게 조절
def softened_error_bounds(x, y, base_error=0.3, slope_factor=0.5):
    dy = np.diff(y)
    dx = np.diff(x)
    raw_slopes = dy / dx
    softened_slopes = np.tanh(np.abs(raw_slopes))
    softened_slopes = np.append(softened_slopes, softened_slopes[-1])
    total_error = base_error + slope_factor * softened_slopes
    return y - total_error, y + total_error

# 계산
lower_raw, upper_raw = raw_error_bounds(x, y)
lower_soft, upper_soft = softened_error_bounds(x, y)

# 시각화
plt.figure(figsize=(10, 5))
plt.plot(x, y, label='Original', color='black')
plt.fill_between(x, lower_raw, upper_raw, color='red', alpha=0.3, label='Raw Error Bounds')
plt.fill_between(x, lower_soft, upper_soft, color='blue', alpha=0.3, label='Softened Error Bounds')
plt.legend()
plt.title("Error Bounds Comparison")
plt.show()