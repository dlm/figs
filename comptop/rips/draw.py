#!/usr/bin/env python

import math
import random

import drawSvg as draw


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        return self.x < other.x or (self.x == other.x and self.y < other.y)

    def dist(self, other):
        dx = self.x-other.x
        dy = self.y-other.y
        return math.sqrt(dx*dx + dy*dy)

class EllipseSampler(object):

    def __init__(self, a, b):
        self.rand = random.Random(1583948955)
        self.a = a
        self.b = b

    def sample(self, noise):
        t = self.rand.uniform(0, 2*math.pi)
        x = self.a * math.cos(t) + self.rand.gauss(0, noise)
        y = self.b * math.sin(t) + self.rand.gauss(0, noise)
        return Point(x,y)

    def filter(self, points, threashold):
        keep = []
        for p in points:
            should_keep = True
            for q in keep:
                should_keep = should_keep and p.dist(q) > threashold
            if should_keep:
                keep.append(p)
        return keep

    def sample_points(self, num_points, noise, filter_dist):
        points = []
        for x in range(num_points):
            points.append(self.sample(noise))

        return self.filter(points, filter_dist)


class RipsDrawer(object):

    def __init__(self, context):
        self.context = context

    def draw_point(self, p):
        c = draw.Circle(p.x, p.y, 1)
        self.context.append(c)

    def draw_ball(self, p, radius):
        c = draw.Circle(
            p.x,
            p.y,
            radius,
            fill='pink',
            fill_opacity=.25,
            stroke_width=.5,
            stroke='black',
        )
        context.append(c)

    def draw_segment(self, p, q):
        c = draw.Line(
            p.x,
            p.y,
            q.x,
            q.y,
            stroke='blue',
            stroke_width=.5,
        )
        self.context.append(c)

    def draw_triangle(self, p, q, r):
        path = draw.Path(
            stroke_opacity=1.0,
            fill='blue',

        )
        path.M(p.x,p.y)  # Start path at point (-30, 5)
        path.l(q.x-p.x,q.y-p.y)  # Draw line to (60, 30)
        path.l(r.x-q.x,r.y-q.y)  # Draw line to (60, 30)
        path.Z()
        self.context.append(path)

    def draw_rips(self, points, dist):
        for p in points:
            self.draw_ball(p, dist/2.0)
            self.draw_point(p)

        for p in points:
            for q in points:
                if not p < q and p.dist(q) < dist:
                    self.draw_segment(p, q)

        for p in points:
            for q in points:
                for r in points:
                    if (p < q and q < r and
                            p.dist(q) < dist and
                            p.dist(r) < dist and
                            q.dist(r) < dist):
                        self.draw_triangle(p, q, r)



num_points = 50
points = EllipseSampler(25,20).sample_points(num_points, noise=3, filter_dist=5)

for dist in range(1,35):
    context = draw.Drawing(100, 100, origin='center')
    RipsDrawer(context).draw_rips(points, dist)
    name = str.format('out/rips-{}.svg', dist)
    context.saveSvg(name)

