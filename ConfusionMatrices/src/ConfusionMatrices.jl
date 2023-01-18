module ConfusionMatrices

export ConfusionMatrix, SimpleConfusionMatrix, SensitivityBasedConfusionMatrix,
	true_positives, false_positives, true_negatives, false_negatives,
	positives, negatives, predicted_positive, predicted_negative, total,
	prevalence,
	true_positive_rate, true_negative_rate, false_positive_rate, false_negative_rate,
	recall, sensitivity, specificity, accuracy, balanced_accuracy,
	positive_predictive_value, negative_predictive_value, precision,
	false_discovery_rate, false_omission_rate,
	positive_likelihood_ratio, negative_likelihood_ratio,
	prevalence_threshold, threat_score, f1_score

"""Abstract base type for all confusion matrices.
In order to implement this interface, you need to have methods
`true_positives`, `false_positives`, `true_negatives`, `false_negatives`,
all accepting an instance of your confusion matrix type
and returning a number.
"""
abstract type ConfusionMatrix end

function true_positives end
function false_positives end
function false_negatives end
function true_negatives end

positives(c::ConfusionMatrix) = true_positives(c) + false_negatives(c)
negatives(c::ConfusionMatrix) = true_negatives(c) + false_positives(c)
predicted_positive(c::ConfusionMatrix) = true_positives(c) + false_positives(c)
predicted_negative(c::ConfusionMatrix) = true_negatives(c) + false_negatives(c)
total(c::ConfusionMatrix) = positives(c) + negatives(c)

prevalence(c::ConfusionMatrix) = positives(c) / total(c)

true_positive_rate(c::ConfusionMatrix) = true_positives(c) / positives(c)
true_negative_rate(c::ConfusionMatrix) = true_negatives(c) / negatives(c)
false_positive_rate(c::ConfusionMatrix) = 1 - true_negative_rate(c)
false_negative_rate(c::ConfusionMatrix) = 1 - true_positive_rate(c)

recall = sensitivity = true_positive_rate
specificity = true_negative_rate

accuracy(c::ConfusionMatrix) = (true_positives(c) + true_negatives(c)) / total(c)
balanced_accuracy(c::ConfusionMatrix) = (true_positive_rate(c) + true_negative_rate(c)) / 2

positive_predictive_value(c::ConfusionMatrix) = true_positives(c) / predicted_positive(c)
negative_predictive_value(c::ConfusionMatrix) = true_negatives(c) / predicted_negative(c)

precision = positive_predictive_value

false_discovery_rate(c::ConfusionMatrix) = 1 - positive_predictive_value(c)
false_omission_rate(c::ConfusionMatrix) = 1 - negative_predictive_value(c)

positive_likelihood_ratio(c::ConfusionMatrix) = true_positive_rate(c) / false_positive_rate(c)
negative_likelihood_ratio(c::ConfusionMatrix) = false_negative_rate(c) / true_negative_rate(c)

prevalence_threshold(c::ConfusionMatrix) = sqrt(false_positive_rate(c)) / (sqrt(true_positive_rate(c)) + sqrt(false_positive_rate(c)))

threat_score(c::ConfusionMatrix) = true_positives(c) / (true_positives(c) + false_negatives(c) + false_positives(c))

f1_score(c::ConfusionMatrix) = 2 * true_positives(c) / (2 * true_positives(c) + false_positives(c) + false_negatives(c))
# concrete confusion matrix types

struct SimpleConfusionMatrix{T <: Number} <: ConfusionMatrix
	true_positives::T
	false_positives::T
	true_negatives::T
	false_negatives::T
end

true_positives(c::SimpleConfusionMatrix) = c.true_positives
false_positives(c::SimpleConfusionMatrix) = c.false_positives
true_negatives(c::SimpleConfusionMatrix) = c.true_negatives
false_negatives(c::SimpleConfusionMatrix) = c.false_negatives

struct SensitivityBasedConfusionMatrix{T <: Number} <: ConfusionMatrix
	sensitivity::T
	specificity::T
	prevalence::T
end

true_positives(c::SensitivityBasedConfusionMatrix) = c.sensitivity * c.prevalence
false_positives(c::SensitivityBasedConfusionMatrix) = (1 - c.specificity) * (1 - c.prevalence)
true_negatives(c::SensitivityBasedConfusionMatrix) = c.specificity * (1 - c.prevalence)
false_negatives(c::SensitivityBasedConfusionMatrix) = (1 - c.sensitivity) * c.prevalence

end # module
