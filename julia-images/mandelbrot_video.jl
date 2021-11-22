using Images, VideoIO

function mandelbrot(colorize::Function, width_pixels::Int, height_pixels::Int; maxiter = 50, threshold = 100, center = -0.63 + 0im, width = 3.2)
    img = RGB{N0f8}.(colorize.(zeros(height_pixels, width_pixels)))
    rows, cols = size(img)
    height = width * rows / cols
    upperleft = center - width / 2 + height / 2 * im
    Threads.@threads for col = 1:cols
        for row = 1:rows
            c = upperleft + col / cols * width - row / rows * height * im
            z = 0
            for i = 1:maxiter
                z = z^2 + c
                if abs2(z) > threshold
                    img[row, col] = colorize(1 - i / maxiter)
                    break
                end
            end
        end
    end
    img
end

let
    local center = -0.743643887037158704752191506114774 + 0.131825904205311970493132056385139im
    local initialwidth = 3.5
    local finalwidth = 1e-30
    local zoom = (x) -> (1 - exp(-20x)) / (1 - exp(-20))
    local nframes = 4000
    encoder_options = (crf = 23, preset = "medium")
    framerate = 25
    frame = function (i)
        α = zoom((i - 1) / (nframes - 1))
        width = α * finalwidth + (1 - α) * initialwidth
        mandelbrot(1920, 1080, maxiter = 200 + 1600 * i / nframes, threshold = 200 + 1600 * i / nframes, center = center, width = width) do x
            RGB{N0f8}((1 - cos(x * 11π)) / 2, (1 - cos(x * 2π)) / 2, (1 - cos(x * 7π)) / 2)
        end
    end
    open_video_out("mandelbrot.mp4", frame(1), framerate = framerate, encoder_options = encoder_options) do writer
        for i = 2:nframes
            write(writer, frame(i))
            println(i)
        end
    end
end