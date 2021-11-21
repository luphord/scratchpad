using Images, VideoIO

function mandelbrot(colorize::Function, width_pixels::Int, height_pixels::Int; maxiter = 50, threshold = 100, center = -0.63 + 0im, width = 3.2)
    img = RGB{N0f8}.(colorize.(zeros(height_pixels, width_pixels)))
    rows, cols = size(img)
    height = width * rows / cols
    upperleft = center - width / 2 + height / 2 * im
    for col = 1:cols
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
    local finalwidth = 1e-4
    local nframes = 100
    local shrinkrate = 1e-2
    encoder_options = (crf = 23, preset = "medium")
    framerate = 25
    frame = function (i)
        width = finalwidth + (initialwidth - finalwidth) * (1 - shrinkrate)^(i - 1)
        mandelbrot(1920, 1080, maxiter = 50, threshold = 100, center = center, width = width) do x
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