using Images, Plots

x = repeat((0:2/199:2)', 200)

img = RGB{Float32}.(x .* x' .* x[:, end:-1:1] .* x[:, end:-1:1]')
save("1.jpg", img)