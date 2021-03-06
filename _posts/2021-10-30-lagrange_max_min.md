---
layout: post
title: Lagrange Duality and Max-Min Inequality
date: 2021-10-30
description: Relating Max-Min Inequality to the Lagrange Duality
---
In this post, we review the Lagrange Duality and give a min-max inequality based interpretation of the duality. We first describe the general optimization problem:
Given any optimization problem (\*) of the form:

$$
\text{minimize} \rm\ f_{0}(x)
$$

$$
\text{s.t.} \; f_{i}(x) \leq 0, \; i=1,\ldots, m \\
$$

$$
h_{i}(x) = 0, \; i=1,\ldots,p
$$

The above problem can be convex problem, non-convex problem, or very well be NP-hard problem. We define the Lagrangian function $$L: \mathbb{R}^{n}\times \mathbb{R}^{m}\times \mathbb{R}^{p} \rightarrow \mathbb{R}$$ as follows:

$$
L(x, \mathbb{\lambda}, \mathbb{\nu}) = f_{0}(x) + \sum_{i=1}^{m}\lambda_{i}f_{i}(x) + \sum_{i=1}^{p}\nu_{i}h_{i}(x)
$$

And the Lagrangian dual function as $$g(\lambda, \nu) = \inf_{x}L(x, \mathbf{\lambda}, \mathbf{\nu})$$. Then, we have the following proposition:


***Proposition 1** : For $$\lambda \geq 0$$, the optimal value of $$g(\lambda, \nu)$$ denoted as $$g(\lambda^{*}, \nu^{*})$$ is the lower-bound on the optimal value of the original problem (\*) denoted as $$f_{0}(x^{*})$$.*


The above can be easily proved using the definition of $$g(\lambda, \nu)$$ and the infimum. We call the original problem (\*) as the primal problem, and define the following optimization problem as the dual problem.

$$
\text{maximize} \;g(\lambda, \nu) \; \text{subject to} \; \lambda \geq 0
$$

We can prove that the dual problem will always be a convex optimization problem.
From Proposition 1, we have $$g(\lambda^{*}, \nu^{*}) \leq f_{0}(x^{*})$$. When this inequality is strict, we call it *Weak Duality*. And when $$(\lambda^{*}, \nu^{*}) = f_{0}(x^{*})$$, we call it the *Strong Duality*. Strong Duality says that solving the dual problem gives the optimal value of the primal problem as well.

We next review the max-min inequality.

***Lemma**: For a function $$\phi(w,z)$$, we have the following inequality*


$$
	\sup_{z \in Z} \inf_{w \in W}\phi(w,z) \leq \inf_{w \in W} \sup_{z \in Z}\phi(w, z)
$$

More information about this inequality can be found at [http://wittawat.com/posts/max_min_inequality.html](http://wittawat.com/posts/max_min_inequality.html).

Next, the max-min inequality can give us the Lagrange Duality. Consider the optimal value of the dual problem $$g(\lambda^{*}, \nu^{*})$$, then

$$
	g(\lambda^{*}, \nu^{*}) = g(\lambda^{*}, \nu^{*}) = \sup_{\lambda \geq 0} g(\lambda, \nu) = \sup_{\lambda \geq 0}\inf_{x}L(x, \lambda, \nu) 
$$

Next consider $$\sup_{\lambda \geq 0} L(x, \lambda, \nu) = \sup_{\lambda \geq 0} f_{0}(x) + \sum_{i=1}^{m}\lambda_{i}f_{i}(x) + \sum_{i=1}^{p}\nu_{i}h_{i}(x)$$ which can be written as

$$
\begin{cases}
f_{0}(x) \rm\ if \rm\ f_{i}(x) \leq 0, \; i=1, \ldots m, \;\; \rm\ and \rm\ h_{i}(x) = 0 \;\; i=1 \ldots p \\\\
\infty \; \text{otherwise}
\end{cases}
$$

Thus, the primal problem can be written as $$\inf_{x}\sup_{\lambda \geq 0}L(x, \lambda, \nu)$$

Then, from the max-min inequality

$$
\sup_{\lambda \geq 0}\inf_{x}L(x, \lambda, \nu) \leq  \inf_{x}\sup_{\lambda \geq 0}L(x, \lambda, \nu)
$$

Or, the solution of the dual problem forms a lower bound on the solution of the primal problem.
Thus, we can derive the Lagrange Duality from the max-min inequality.