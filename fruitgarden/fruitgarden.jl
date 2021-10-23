### A Pluto.jl notebook ###
# v0.16.1

using Markdown
using InteractiveUtils

# ╔═╡ b43c2d80-ee70-49db-8dfb-3a9bb968eb89
using Statistics

# ╔═╡ 51869554-3412-11ec-37cd-9dfcf79c8a92
mutable struct FruitGardenState
	raven::Int
	fruits::Array{Int}
	rounds::Int
end

# ╔═╡ 9ef9b517-5a0d-41da-a8ab-2a2919f09a91
function simulate_round(state::FruitGardenState)
	x = rand(1:6)
	if x == 6
		state.raven += 1
	elseif x == 5
		highest = argmax(state.fruits)
		state.fruits[highest] = max(state.fruits[highest] - 1, 0)
	elseif x in 1:4
		state.fruits[x] = max(state.fruits[x] - 1, 0)
	else
		throw("invalid state")
	end
	state.rounds += 1
	return state
end

# ╔═╡ 7090d5f6-d3e4-40d4-af63-36fd42c9c238
function isover(state::FruitGardenState)
	return state.raven >= 6 || sum(state.fruits) <= 0
end

# ╔═╡ 0f5005b2-d4e8-498d-a50d-694237c48b68
begin
	n = 100000
	won = zeros(Int, n)
	rounds = zeros(Int, n)
	for i in 1:n
		state = FruitGardenState(1, [4, 4, 4, 4], 0)
		while !isover(state)
			simulate_round(state)
		end
		won[i] = sum(state.fruits) <= 0
		rounds[i] = state.rounds
	end
	mean(won), mean(rounds), std(rounds)
end

# ╔═╡ 00000000-0000-0000-0000-000000000001
PLUTO_PROJECT_TOML_CONTENTS = """
[deps]
Statistics = "10745b16-79ce-11e8-11f9-7d13ad32a3b2"
"""

# ╔═╡ 00000000-0000-0000-0000-000000000002
PLUTO_MANIFEST_TOML_CONTENTS = """
# This file is machine-generated - editing it directly is not advised

[[Libdl]]
uuid = "8f399da3-3557-5675-b5ff-fb832c97cbdb"

[[LinearAlgebra]]
deps = ["Libdl"]
uuid = "37e2e46d-f89d-539d-b4ee-838fcccc9c8e"

[[Random]]
deps = ["Serialization"]
uuid = "9a3f8284-a2c9-5f02-9a11-845980a1fd5c"

[[Serialization]]
uuid = "9e88b42a-f829-5b0c-bbe9-9e923198166b"

[[SparseArrays]]
deps = ["LinearAlgebra", "Random"]
uuid = "2f01184e-e22b-5df5-ae63-d93ebab69eaf"

[[Statistics]]
deps = ["LinearAlgebra", "SparseArrays"]
uuid = "10745b16-79ce-11e8-11f9-7d13ad32a3b2"
"""

# ╔═╡ Cell order:
# ╠═b43c2d80-ee70-49db-8dfb-3a9bb968eb89
# ╠═51869554-3412-11ec-37cd-9dfcf79c8a92
# ╠═9ef9b517-5a0d-41da-a8ab-2a2919f09a91
# ╠═7090d5f6-d3e4-40d4-af63-36fd42c9c238
# ╠═0f5005b2-d4e8-498d-a50d-694237c48b68
# ╟─00000000-0000-0000-0000-000000000001
# ╟─00000000-0000-0000-0000-000000000002
