#Імпорт необхідних бібліотек
import numpy as np
import matplotlib.pyplot as plt

#Вихідні дані лабораторної роботи відповідно до варіанту
lam = 3.2 #довжина хвилі
a = 12 #розмір розкриву у площині H
b = 16 #розмір розкриву у площині E
theta_deg = np.linspace(-90, 90, 10000) #кут -90; 90
theta = np.radians(theta_deg) #кут переведений до радіан


#Розрахунок діаграми у площині H
core_H = np.where(np.abs(1 - (2 * a / lam * np.sin(theta))**2) < 1e-10, np.pi/4,
                  np.cos(np.pi * a / lam * np.sin(theta)) / (1 - (2 * a / lam * np.sin(theta))**2))
FH = core_H * (1 + np.cos(theta)) / 2

#Розрахунок діаграми у площині E
x = np.pi * b / lam * np.sin(theta)
FE = np.sinc(x / np.pi) * (1 + np.cos(theta)) / 2

#Нормування діаграм
FH_norm = np.abs(FH) / np.max(np.abs(FH))
FE_norm = np.abs(FE) / np.max(np.abs(FE))

#Визначення нулів та максимумів бокових пелюсток
def find_extr(F, angles):
    maxi, mini = [], []

    for i in range(1, len(F) - 1):
        if F[i] > F[i - 1] and F[i] > F[i + 1]:
            maxi.append(i)
        elif F[i] < F[i - 1] and F[i] < F[i + 1]:
            mini.append(i)
    return maxi, mini

max_H, min_H = find_extr(FH_norm, theta_deg)
max_E, min_E = find_extr(FE_norm, theta_deg)

#Знаходження ширини головної пелюстки на рівні 0,707
def get_width(F, angles):
    c = np.argmax(F)

    idx_left = np.where(F[:c] <= 0.707)[0]
    left = angles[idx_left[-1]] if len(idx_left) > 0 else None
    idx_right = np.where(F[c:] <= 0.707)[0]
    right = angles[c + idx_right[0]] if len(idx_right) > 0 else None

    return right - left

width_H = get_width(FH, theta_deg)
width_E = get_width(FE, theta_deg)

#розрахунок теоретичної ширини для порівняння
th_width_H = 68 * lam / a
th_width_E = 51 * lam / b

#розрахунок КСД
Dm = 0.81 * (4 * np.pi / lam**2) * a * b

#Виведення результатів розрахунків
print(f"\nШирина головної пелюстки у площині H: {width_H:.3f} град.; теоретична: {th_width_H:.3f} град.")
print(f"Ширина головної пелюстки у площині E: {width_E:.3f} град.; теоретична: {th_width_E:.3f} град.")
print(f"КСД ≈ {Dm:.3f}")

print("\nМаксимуми бокових пелюсток у площині H:")
for i in max_H:
    print(f"θ = {theta_deg[i]:.3f} град., рівень = {FH_norm[i]:.4f}")

print("\nМаксимуми бокових пелюсток у площині E:")
for i in max_E:
    print(f"θ = {theta_deg[i]:.3f} град., рівень = {FE_norm[i]:.4f}")

print("\nНулі у площині H:")
for i in min_H:
    if FH_norm[i] < 0.05:
        print(f"θ = {theta_deg[i]:.3f} град.")

print("\nНулі у площині E:")
for i in min_E:
    if FE_norm[i] < 0.05:
        print(f"θ = {theta_deg[i]:.3f} град.")

th_tab = np.arange(0, 90.1, 5)
FH_tab = np.interp(th_tab, theta_deg, FH_norm)
FE_tab = np.interp(th_tab, theta_deg, FE_norm)

print("\nθ, град | F_H(θ) | F_E(θ)")
for i in range(len(th_tab)):
  print(f"{th_tab[i]:6.1f} | {FH_tab[i]:8.4f} | {FE_tab[i]:8.4f}")


#Побудова графіків
#нормована ДС
plt.figure(figsize=(10, 6))
plt.plot(theta_deg, FH_norm, label="F_H(θ)")
plt.plot(theta_deg, FE_norm, label="F_E(θ)")
plt.axhline(0.707, linestyle="--", label="0.707")
plt.xlabel("θ, градуси")
plt.ylabel("Нормована ДС")
plt.title("Нормовані ДС у площинах H та E")
plt.grid()
plt.legend()
plt.xlim(0, 90)
plt.ylim(0, 1)
plt.savefig("ДС у площині Н та Е.png", dpi=300)
plt.show()

#радіальна ДС
fig2 = plt.figure(figsize=(8, 8))
ax = fig2.add_subplot(111, projection="polar")
ax.plot(theta, FH_norm, label="$F_H(θ)$")
ax.plot(theta, FE_norm, label="$F_E(θ)$")
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_thetagrids(range(0, 360, 10))
ax.set_title("Радіальні ДС у площинах H та E")
ax.legend()
plt.savefig("ДС радіальна.png", dpi=300)
plt.show()